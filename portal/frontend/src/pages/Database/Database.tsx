import React, { useContext, useEffect, useState, useRef } from 'react';
import { Alert, Skeleton } from '@mui/material';
import BaseLayout from '../../components/BaseLayout/BaseLayout';
import UploadFile from './UploadFile/UploadFile';
import ProcessingFile from './ProcessingFile/ProcessingFile';
import OriginalSamples from './OriginalSamples/OriginalSamples';
import { AuthContext } from '../../AuthContext';
import { checkProcessingStatus } from '../../services/operations';

// Enum para os status de processamento
enum ProcessingStatus {
  Error = -3,
  Loading = -2,
  WaitingForProcessing = -1,
  Processing = 0,
  Processed = 1,
  UsingAggregatedDatabase = 2,
}

const Database: React.FC = () => {
  const [processingStatus, setProcessingStatus] = useState(
    ProcessingStatus.Loading,
  );
  const { isUsingAggregatedDatabase, setIsUsingAggregatedDatabase } =
    useContext(AuthContext);
  const context = useContext(AuthContext);

  const intervalId = useRef<NodeJS.Timeout | null>(null);

  const handleAggregateDatabaseClick = () => {
    setProcessingStatus(ProcessingStatus.UsingAggregatedDatabase);
    setIsUsingAggregatedDatabase(!isUsingAggregatedDatabase);
  };

  const fetchData = async () => {
    try {
      const response = await checkProcessingStatus(context?.user?.email ?? '');
      setProcessingStatus(response);
    } catch (error) {
      console.error('Erro ao verificar o status de processamento:', error);
      setProcessingStatus(ProcessingStatus.Error);
    }
  };

  useEffect(() => {
    fetchData();
    console.log('🚀 ~ useEffect ~ fetchData:');

    // Define o intervalo para verificar o status a cada 3 horas
    intervalId.current = setInterval(fetchData, 3 * 60 * 60 * 1000);

    // Limpa o intervalo ao desmontar o componente
    return () => {
      if (intervalId.current) {
        clearInterval(intervalId.current);
      }
    };
  }, []);

  const handleUploadComplete = () => {
    fetchData();
  };

  // Renderização condicional com base no status de processamento
  return (
    <BaseLayout>
      {processingStatus === ProcessingStatus.Error && (
        <>
          <UploadFile
            isComplete={false}
            onUploadComplete={handleUploadComplete}
            onAggregateDatabaseClick={handleAggregateDatabaseClick}
          />
          <Alert severity="error">
            Erro ao verificar o status do processamento.
          </Alert>
        </>
      )}
      {processingStatus === ProcessingStatus.Loading && (
        <Skeleton variant="rectangular" height={700} />
      )}
      {processingStatus === ProcessingStatus.WaitingForProcessing && (
        <UploadFile
          isComplete
          onUploadComplete={handleUploadComplete}
          onAggregateDatabaseClick={handleAggregateDatabaseClick}
        />
      )}
      {processingStatus === ProcessingStatus.Processing && (
        <>
          <UploadFile
            isComplete={false}
            onUploadComplete={handleUploadComplete}
            onAggregateDatabaseClick={handleAggregateDatabaseClick}
          />
          <ProcessingFile />
        </>
      )}
      {(processingStatus === ProcessingStatus.Processed ||
        processingStatus === ProcessingStatus.UsingAggregatedDatabase) && (
        <>
          <UploadFile
            isComplete={false}
            onUploadComplete={handleUploadComplete}
            onAggregateDatabaseClick={handleAggregateDatabaseClick}
          />
          <OriginalSamples />
        </>
      )}
    </BaseLayout>
  );
};

export default Database;
