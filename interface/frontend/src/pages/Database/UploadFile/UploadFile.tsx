import React, { useState, useContext } from 'react';
import { styled } from '@mui/material/styles';
import {
  Container,
  Button,
  Typography,
  CircularProgress,
  Box,
  Alert,
} from '@mui/material';
import { AuthContext } from '../../../AuthContext';
import { sendFile } from '../../../services/operations';

const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
});

interface UploadFileProps {
  isComplete: boolean;
  onUploadComplete: () => void;
  onAggregateDatabaseClick: () => void;
}

const UploadFile: React.FC<UploadFileProps> = ({
  isComplete,
  onUploadComplete,
  onAggregateDatabaseClick,
}) => {
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { user, isUsingAggregatedDatabase } = useContext(AuthContext);

  const handleFileChange = async (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    const selectedFile = event.target.files ? event.target.files[0] : null;
    setFile(selectedFile);

    if (selectedFile) {
      const fileExtension = selectedFile.name.split('.').pop()?.toLowerCase();

      if (fileExtension === 'pcap') {
        setIsLoading(true);
        setError(null);

        try {
          await sendFile(selectedFile, user?.email ?? '');
          onUploadComplete();
        } catch (error) {
          console.error('Erro ao enviar o arquivo:', error);
          setError('Erro ao enviar o arquivo. Por favor, tente novamente.');
        } finally {
          setIsLoading(false);
        }
      } else {
        setError('Formato de arquivo inválido. Selecione um arquivo .pcap.');
        setIsLoading(false);
      }
    }
  };

  const renderUploadButton = () => (
    <Button
      component="label"
      variant="contained"
      sx={{
        minHeight: 60,
        backgroundColor: '#333333',
      }}
      disabled={isLoading}
    >
      {isLoading ? 'Carregando...' : 'Carregar base de dados'}
      <VisuallyHiddenInput type="file" onChange={handleFileChange} />
    </Button>
  );

  return (
    <Container maxWidth={false} sx={{ color: 'black', textAlign: 'left' }}>
      {error && <Alert severity="error">{error}</Alert>}

      <Container
        maxWidth="md"
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: isComplete ? '80vh' : 'auto',
          textAlign: 'center',
          color: 'black',
          marginTop: '1vh',
        }}
      >
        <Typography variant="h3" gutterBottom>
          Carregamento da base de dados
        </Typography>

        {/* Exibe a mensagem apenas se isComplete for true */}
        {isComplete && (
          <Typography variant="h5" paragraph>
            Selecione uma base de dados. O Dust irá realizar o processamento
            inicial e mostrar características interessantes a partir de técnicas
            de aprendizagem de máquina.
          </Typography>
        )}

        <Box
          sx={{
            display: 'flex',
            gap: 2,
            mt: 2,
            width: '100%',
            justifyContent: 'center',
          }}
        >
          {/* Botão para carregar base de dados agregada */}
          <Button
            variant="contained"
            sx={{
              minHeight: 60,
              backgroundColor: '#333333',
            }}
            disabled={isLoading}
            onClick={onAggregateDatabaseClick}
          >
            {isUsingAggregatedDatabase
              ? 'Remover base agregada'
              : 'Carregar base agregada'}
          </Button>

          {/* Botão para carregar arquivo */}
          {renderUploadButton()}
        </Box>

        {isLoading && <CircularProgress sx={{ mt: 2 }} />}

        {/* Exibe o nome do arquivo apenas se o arquivo foi carregado e não há erro */}
        {file && !isLoading && !error && (
          <Typography variant="subtitle1" sx={{ color: 'green', mt: 2 }}>
            Arquivo carregado: {file.name}
          </Typography>
        )}

        <Typography variant="h6" sx={{ mt: 4 }}>
          A base deve ser no formato PCAP, e não deve ultrapassar 1GB.
        </Typography>
      </Container>
    </Container>
  );
};

export default UploadFile;
