import {
  uploadFile,
  getProcessingStatus,
  getJSONData,
  getDefenseData,
} from './service';

// Função para enviar o arquivo
export const sendFile = async (file: File, email: string) => {
  try {
    await uploadFile(file, email);
  } catch (error) {
    console.error('Erro ao enviar arquivo:', error);
    throw error;
  }
};

// Função para verificar o status de processamento
export const checkProcessingStatus = async (email: string) => {
  try {
    const status = await getProcessingStatus(email);
    return status;
  } catch (error) {
    console.error('Erro ao verificar o status de processamento:', error);
    throw error;
  }
};

// Função para ler os dados JSON
export const readJSONData = async (email: string) => {
  try {
    const jsonData = await getJSONData(email);
    return jsonData;
  } catch (error) {
    console.error('Erro ao ler os dados JSON:', error);
    throw error;
  }
};

// Função para ler os dados de defesa
export const readDefenseData = async (email: string) => {
  try {
    const defenseData = await getDefenseData(email);
    return defenseData;
  } catch (error) {
    console.error('Erro ao ler os dados de defesa:', error);
    throw error;
  }
};
