import React from 'react';
import {
  Box,
  Container,
  Divider,
  Typography,
  CircularProgress,
  Stack,
  ListItemText,
} from '@mui/material';

const ProcessingFile: React.FC = () => (
  <Container maxWidth={false} sx={{ color: 'black', textAlign: 'left' }}>
    <Box sx={{ mt: 2, mb: 2 }}>
      <Stack
        direction="row"
        justifyContent="center"
        alignItems="center"
        spacing={2}
      >
        <CircularProgress />
        <Typography variant="h4" gutterBottom>
          Carregando o dataset e gerando as primeiras análises, isso pode levar
          algum tempo...{' '}
        </Typography>
      </Stack>
    </Box>
    <Divider />

    <Box sx={{ my: 2 }}>
      <Typography variant="h6" gutterBottom>
        Nesse momento, o Dust fará uso de uma rede neural para diferenciar os
        pacotes em duas categorias:
      </Typography>
      <ul>
        <li>
          <ListItemText
            primary={
              <Typography variant="h5" fontWeight="bold">
                Dados
              </Typography>
            }
          />
        </li>
        <li>
          <ListItemText
            primary={
              <Typography variant="h5" fontWeight="bold">
                Ataque (em potencial)
              </Typography>
            }
          />
        </li>
      </ul>
    </Box>
    <Divider />

    {/* Seção 2: Etapa do Processamento */}
    <Box sx={{ my: 2 }}>
      <Typography variant="h6" gutterBottom>
        Após o carregamento do dataset, ocorrerá um processo de
        identificação,balanceamento e transformação.
      </Typography>
      <ul>
        <li>
          <ListItemText
            primary={
              <Typography variant="h5">
                <strong>Identificação:</strong> Classificação dos pacotes como
                dados ou ataque.
              </Typography>
            }
          />
        </li>
        <li>
          <ListItemText
            primary={
              <Typography variant="h5">
                <strong>Balanceamento:</strong> Os registros são balanceados
                através de um mecanismo de upscaling.
              </Typography>
            }
          />
        </li>
        <li>
          <ListItemText
            primary={
              <Typography variant="h5">
                <strong>Transformação:</strong> São extraídas 20 características
                da base de dados, utilizadas para treinar a rede neural que é
                usada no processo que gera as amostras adversárias
              </Typography>
            }
          />
        </li>
      </ul>
    </Box>
    <Divider />

    <Box sx={{ my: 2 }}>
      <Typography variant="h6" gutterBottom>
        Finalmente, ocorre o treinamento da rede neural a partir das 20
        características, abaixo está uma descrição resumida de sua aplicação,
        utilizando camadas da biblioteca Pytorch
      </Typography>
      <ul>
        <li>
          <ListItemText
            primary={
              <Typography variant="h5" fontWeight="bold">
                LeakyReLU(Linear(20, 64))
              </Typography>
            }
          />
        </li>
        <li>
          <ListItemText
            primary={
              <Typography variant="h5" fontWeight="bold">
                LeakyReLU(BatchNorm1d(Linear(64, 128)))
              </Typography>
            }
          />
        </li>
        <li>
          <ListItemText
            primary={
              <Typography variant="h5" fontWeight="bold">
                LeakyReLU(BatchNorm1d(Linear(128, 256)))
              </Typography>
            }
          />
        </li>
        <li>
          <ListItemText
            primary={
              <Typography variant="h5" fontWeight="bold">
                LeakyReLU(BatchNorm1d(Linear(128, 256)))
              </Typography>
            }
          />
        </li>
        <li>
          <ListItemText
            primary={
              <Typography variant="h5" fontWeight="bold">
                Tanh()
              </Typography>
            }
          />
        </li>
        <li>
          <ListItemText
            primary={
              <Typography variant="h5" fontWeight="bold">
                BatchNorm1d(Linear(256, 20))
              </Typography>
            }
          />
        </li>
        <li>
          <ListItemText
            primary={
              <Typography variant="h5" fontWeight="bold">
                Linear(20, 2)
              </Typography>
            }
          />
        </li>
      </ul>
    </Box>
    <Divider />

    <Box sx={{ my: 2 }}>
      <Typography variant="h6" gutterBottom>
        Assim que o processamento for concluído, as informações sobre a rede
        neural treinada serão exibidas nesta página.
      </Typography>
    </Box>
  </Container>
);

export default ProcessingFile;
