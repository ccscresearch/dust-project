import React, { useContext, useEffect, useState } from 'react';
import {
  Alert,
  Box,
  Card,
  Container,
  Divider,
  Grid,
  Typography,
  Skeleton,
} from '@mui/material';
import ConfusionMatrixPlot from '../../features/ConfusionMatrixPlot/ConfusionMatrixPlot';
import SampleDistributionGraph from '../../features/SampleDistributionGraph/SampleDistributionGraph';
import { styles } from '../../pages/AdversarialSamples/style';
import { readJSONData } from '../../services/operations';
import { AuthContext } from '../../AuthContext';
import results from '../../data/results.json';

interface ConfusionMatrixContainerProps {
  dataType: 'original' | 'adversarial';
  source: 'uploaded' | 'aggregated';
}

// Interface Data mantida como no JSON original
interface Data {
  labels_map: { [key: string]: string };
  accuracies: {
    adversaries: number;
    original: number;
  };
  confMat_by_percentage: number[][];
  confMat_by_instances: number[][];
  confMatOriginal_by_percentage: number[][];
  confMatOriginal_by_instances: number[][];
  sizes: {
    original: {
      dataset: number;
      [key: string]: number;
    };
    upscaled: {
      dataset: number;
      [key: string]: number;
    };
  };
}

const ConfusionMatrixContainer: React.FC<ConfusionMatrixContainerProps> = ({
  dataType,
  source,
}) => {
  const { user } = useContext(AuthContext);
  const [data, setData] = useState<Data | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setError(null);
      try {
        const response = await readJSONData(user?.email ?? '');

        if (isValidData(response)) {
          setData(response);
        } else {
          setError('Os dados recebidos são inválidos.');
        }
      } catch (error) {
        console.error('Erro ao carregar dados:', error);
        setError('Erro ao carregar dados. Por favor, tente novamente.');
      }
    };

    const isValidData = (data: unknown): data is Data => {
      // Validação de dados adaptada aos nomes do JSON
      return (
        typeof data === 'object' &&
        data !== null &&
        'labels_map' in data &&
        'accuracies' in data &&
        'confMat_by_percentage' in data &&
        'confMat_by_instances' in data &&
        'confMatOriginal_by_percentage' in data &&
        'confMatOriginal_by_instances' in data &&
        'sizes' in data
      );
    };

    if (source === 'aggregated') {
      setData(results);
    } else {
      fetchData();
    }
  }, [dataType, source, user?.email]);

  // Lógica para acessar os dados corretos do JSON
  const accuracy =
    dataType === 'original'
      ? data?.accuracies.original
      : data?.accuracies.adversaries;
  const matrixData =
    dataType === 'original'
      ? data?.confMatOriginal_by_percentage
      : data?.confMat_by_percentage;
  const totalInstances =
    dataType === 'original'
      ? data?.sizes.original.dataset
      : data?.sizes.upscaled.dataset;
  const dataInstances =
    dataType === 'original'
      ? data?.sizes.original['0']
      : data?.sizes.upscaled['0'];
  const attackInstances =
    dataType === 'original'
      ? data?.sizes.original['1']
      : data?.sizes.upscaled['1'];
  const dataSizes =
    dataType === 'original' ? data?.sizes.original : data?.sizes.upscaled;

  return (
    <Container maxWidth={false} sx={{ px: 1 }}>
      {error ? (
        dataType === 'original' ? (
          <Alert severity="error">{error}</Alert>
        ) : (
          <>
            <Alert severity="warning">
              Ainda não foram carregados arquivos ou o processamento não foi
              concluído.
            </Alert>
          </>
        )
      ) : data ? (
        <>
          {dataType === 'adversarial' &&
            (source === 'uploaded' || source === 'aggregated') && (
              <>
                <Typography variant="h3" sx={styles.title}>
                  Classes identificadas nas amostras adversárias
                </Typography>
                <Divider sx={{ marginBottom: '2rem' }} />
                <Card variant="outlined" sx={styles.card}>
                  <Typography variant="h6" gutterBottom>
                    Ao todo, foram geradas {totalInstances} amostras
                    adversárias, sendo {dataInstances} de ataque e{' '}
                    {attackInstances} de dados. O modelo previamente treinado
                    apresentou uma queda de{' '}
                    {data.accuracies.original.toFixed(2)}% para{' '}
                    {data.accuracies.adversaries.toFixed(2)}% em sua acurácia de
                    classificação quando confrontado com as amostras geradas.
                  </Typography>
                </Card>
              </>
            )}

          {dataType === 'original' &&
            (source === 'uploaded' || source === 'aggregated') && (
              <>
                <Typography variant="h3" sx={{ ...styles.title, mt: 5 }}>
                  Diversificação de dados detectada pela rede neural
                </Typography>
                <Divider sx={{ marginBottom: '2rem' }} />
                <Card variant="outlined" sx={styles.card}>
                  <Typography variant="h6" gutterBottom>
                    Foram encontrados {dataInstances} instâncias de pacotes de
                    dados, e {attackInstances} instâncias potencialmente
                    identificadas como atacantes.
                  </Typography>
                  <Divider sx={{ margin: '1rem 0' }} />
                  <Typography variant="h6" gutterBottom>
                    Treinando a rede neural com esses registros, ela foi capaz
                    de classificar com {data.accuracies.original.toFixed(2)}% na
                    classe correta.
                  </Typography>
                  <Divider sx={{ margin: '1rem 0' }} />
                  <Typography variant="h6" gutterBottom>
                    Essa mesma rede neural é utilizada para gerar as amostras
                    adversárias, que confrontam o modelo de defesa proposto.
                  </Typography>
                </Card>
              </>
            )}

          <Box
            display="flex"
            flexDirection="column"
            alignItems="center"
            justifyContent="center"
          >
            <Box sx={{ flexGrow: 1 }}>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  {dataSizes && (
                    <SampleDistributionGraph
                      labels={data.labels_map}
                      dataSizes={dataSizes}
                    />
                  )}
                </Grid>
                <Grid
                  item
                  xs={6}
                  container
                  alignItems="center"
                  justifyContent="center"
                >
                  <ConfusionMatrixPlot
                    isOriginal={dataType === 'original'}
                    title="Acurácia de identificação automática das classes na base"
                    accuracy={accuracy ?? 0}
                    matrixData={matrixData || []}
                    labels={data.labels_map}
                    originalAccuracy={data.accuracies.original}
                  />
                </Grid>
              </Grid>
            </Box>
          </Box>
        </>
      ) : (
        // Esqueletos para carregamento
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <Skeleton variant="rectangular" height={50} />
          <Skeleton variant="rectangular" height={200} />
          <Skeleton variant="rectangular" height={300} />
        </Box>
      )}
    </Container>
  );
};

export default ConfusionMatrixContainer;
