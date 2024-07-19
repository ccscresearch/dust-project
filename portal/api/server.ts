import * as admin from "firebase-admin";
import express, { Request, Response } from "express";
import multer from "multer";
import cors from "cors";
import fs from "fs";
import path from "path";

const port = process.env.PORT || 3001;
const app = express();

// Configuração do CORS
app.use(
  cors({
    origin: "http://localhost:5173",
    methods: ["GET", "POST", "PUT", "DELETE"],
    allowedHeaders: ["Content-Type", "Authorization"],
  })
);

// Configuração do Multer para upload de arquivos
const storage = multer.diskStorage({
  destination: "./uploads/", // Pasta de uploads
  filename: (req, file, cb) => {
    cb(null, `${Date.now()}-${file.originalname}`);
  },
});
const upload = multer({ storage });

app.use(express.json());

// Função auxiliar para formatar o email
const formatEmail = (email: string) => email.replace(/[@.]/g, "_");

// Função auxiliar para encontrar o arquivo mais recente em um diretório
const findLatestFile = (dir: string, ext: string): string | null => {
  try {
    const files = fs.readdirSync(dir);
    const filteredFiles = files.filter((file) => file.endsWith(ext));
    if (filteredFiles.length === 0) {
      return null;
    }
    return filteredFiles.sort(
      (a, b) =>
        fs.statSync(path.join(dir, b)).mtime.getTime() -
        fs.statSync(path.join(dir, a)).mtime.getTime()
    )[0];
  } catch (error) {
    console.error(`Erro ao encontrar o arquivo mais recente em ${dir}:`, error);
    return null;
  }
};

// Rota para upload de arquivos
app.post(
  "/upload",
  upload.single("arquivo"),
  async (req: Request, res: Response) => {
    try {
      const { email, nomeArquivo } = req.body;
      const file = req.file;

      if (!file) {
        return res.status(400).send("Nenhum arquivo enviado.");
      }

      const formattedEmail = formatEmail(email);
      const userDir = `./uploads/${formattedEmail}`;

      // Cria a pasta do usuário se não existir
      if (!fs.existsSync(userDir)) {
        fs.mkdirSync(userDir, { recursive: true });
      }

      // Move o arquivo para a pasta do usuário
      const filePath = path.join(userDir, file.filename);
      fs.renameSync(file.path, filePath);

      console.log(`Arquivo ${file.filename} salvo com sucesso para ${email}!`);
      return res.send("Arquivo salvo com sucesso!");
    } catch (error) {
      console.error("Erro ao fazer upload do arquivo:", error);
      return res.status(500).send("Erro ao fazer upload do arquivo.");
    }
  }
);

// Rota para verificar o status de processamento do arquivo
app.get("/processingStatus", async (req: Request, res: Response) => {
  try {
    const email = req.query.email as string;
    const formattedEmail = formatEmail(email);
    const userDir = `./uploads/${formattedEmail}`;

    // Verifica se a pasta do usuário existe
    if (!fs.existsSync(userDir)) {
      return res.status(404).send("-1"); // Usuário não encontrado
    }

    const latestFile = findLatestFile(userDir, "");

    // Verifica se há arquivos na pasta
    if (!latestFile) {
      return res.status(200).send("-1"); // Nenhum arquivo encontrado
    }

    const ext = path.extname(latestFile);

    // Verifica o status de processamento com base na extensão do arquivo
    if (ext === ".pcap") {
      return res.status(200).send("0"); // Arquivo PCAP encontrado, aguardando processamento
    } else if (ext === ".json") {
      return res.status(200).send("1"); // Arquivo JSON encontrado, processamento concluído
    } else {
      return res.status(200).send("-1"); // Nenhum arquivo válido encontrado
    }
  } catch (error) {
    console.error("Erro ao verificar o status de processamento:", error);
    return res.status(500).send("Erro ao verificar o status de processamento.");
  }
});

// Rota para obter o arquivo JSON do banco de dados
app.get("/databaseJSONFile", (req: Request, res: Response) => {
  try {
    const email = req.query.email as string;
    const formattedEmail = formatEmail(email);
    const userDir = `./uploads/${formattedEmail}`;

    // Encontra o arquivo JSON mais recente
    const latestJsonFile = findLatestFile(userDir, ".json");

    if (!latestJsonFile) {
      return res.status(404).send("Nenhum arquivo JSON encontrado.");
    }

    const filePath = path.join(userDir, latestJsonFile);

    // Lê o arquivo JSON e envia como resposta
    fs.readFile(filePath, "utf8", (err, data) => {
      if (err) {
        console.error("Erro ao ler o arquivo JSON:", err);
        return res.status(500).send("Erro ao ler o arquivo JSON.");
      }
      const jsonData = JSON.parse(data);
      res.json(jsonData);
    });
  } catch (error) {
    console.error("Erro ao obter o arquivo JSON do banco de dados:", error);
    res.status(500).send("Erro ao obter o arquivo JSON do banco de dados.");
  }
});

// Rota para obter o arquivo JSON do modelo de defesa
app.get("/defenseJSONFile/", (req: Request, res: Response) => {
  try {
    const email = req.query.email as string;
    const formattedEmail = formatEmail(email);
    const userDir = `./defenseModel/${formattedEmail}`;

    // Encontra o arquivo JSON mais recente
    const latestJsonFile = findLatestFile(userDir, ".json");

    if (!latestJsonFile) {
      return res.status(404).send("Nenhum arquivo JSON encontrado.");
    }

    const filePath = path.join(userDir, latestJsonFile);

    // Lê o arquivo JSON e envia como resposta
    fs.readFile(filePath, "utf8", (err, data) => {
      if (err) {
        console.error("Erro ao ler o arquivo JSON:", err);
        return res.status(500).send("Erro ao ler o arquivo JSON.");
      }
      const jsonData = JSON.parse(data);
      res.json(jsonData);
    });
  } catch (error) {
    console.error("Erro ao obter o arquivo JSON do modelo de defesa:", error);
    res.status(500).send("Erro ao obter o arquivo JSON do modelo de defesa.");
  }
});

app.listen(port, () => {
  console.log(`Servidor rodando na porta ${port}`);
});
