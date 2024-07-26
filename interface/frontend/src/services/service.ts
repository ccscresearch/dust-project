import axios from 'axios';

// Configuração base da URL da API
const api = axios.create({
  baseURL: 'http://localhost:3001',
});

// Função para enviar o arquivo
export const uploadFile = async (file: File, email: string) => {
  try {
    const formData = new FormData();
    formData.append('arquivo', file);
    formData.append('nomeArquivo', file.name);
    formData.append('email', email);

    const response = await api.post('/upload', formData);
    console.log('Arquivo enviado com sucesso:', response.data);
  } catch (error) {
    console.error('Erro ao enviar arquivo:', error);
    throw error;
  }
};

// Função para obter o status de processamento
export const getProcessingStatus = async (email: string) => {
  try {
    const response = await api.get(`/processingStatus?email=${email}`);
    return response.data;
  } catch (error) {
    console.error('Erro ao obter status de processamento:', error);
    throw error;
  }
};

// Função para obter os dados JSON
export const getJSONData = async (email: string) => {
  try {
    const response = await api.get(`/databaseJSONFile?email=${email}`);
    return response.data;
  } catch (error) {
    console.error('Erro ao obter dados JSON:', error);
    throw error;
  }
};

// Função para obter os dados de defesa
export const getDefenseData = async (email: string) => {
  try {
    const response = await api.get(`/defenseJSONFile?email=${email}`);
    return response.data;
  } catch (error) {
    console.error('Erro ao obter dados de defesa:', error);
    throw error;
  }
};
