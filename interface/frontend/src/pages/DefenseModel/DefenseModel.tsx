/* eslint-disable react/react-in-jsx-scope */
import { useContext, useEffect, useState } from 'react';
import { AuthContext } from '../../AuthContext';
import BaseLayout from '../../components/BaseLayout/BaseLayout';
import {
  Alert,
  Box,
  Card,
  Container,
  Divider,
  Grid,
  Paper,
  Skeleton,
  Stack,
  Typography,
} from '@mui/material';
import { styles } from './style';
import { readDefenseData } from '../../services/operations';
import SampleDistributionGraph from '../../features/SampleDistributionGraph/SampleDistributionGraph';
import results from '../../data/defense.json';

interface Data {
  qdtePortscan: number;
  qtdeDados: number;
  labels_map: { [key: string]: string };
  accuracies?: {
    adversaries: number;
    original: number;
  };
  confMat_by_percentage?: number[][];
  confMat_by_instances?: number[][];
  confMatOriginal_by_percentage?: number[][];
  confMatOriginal_by_instances?: number[][];
}

function DefenseModel() {
  const context = useContext(AuthContext);
  const [data, setData] = useState<Data | null>(null);
  const [isLoading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { isUsingAggregatedDatabase } = useContext(AuthContext);

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await readDefenseData(context?.user?.email ?? '');
      setData(response);
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      setError('Erro ao carregar dados.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isUsingAggregatedDatabase) {
      setData(results);
    } else {
      fetchData();
    }
    setLoading(false);
  }, [isUsingAggregatedDatabase]);

  const total = (data?.qdtePortscan ?? 0) + (data?.qtdeDados ?? 0);
  const attackPercentage =
    total > 0 ? ((data?.qdtePortscan ?? 0) / total) * 100 : 0;
  const dataPercentage = total > 0 ? ((data?.qtdeDados ?? 0) / total) * 100 : 0;
  const dataSizes = {
    dataset: total,
    '0': data?.qtdeDados ?? 0,
    '1': data?.qdtePortscan ?? 0,
  };

  if (isLoading) {
    return (
      <BaseLayout>
        <Container
          maxWidth={false}
          sx={{ px: 1, pt: { xs: '1vh', sm: '1vh', md: '2vh' } }}
        >
          <Skeleton variant="rectangular" sx={{ mt: '1vh' }} height={100} />
          <Skeleton variant="rectangular" sx={{ mt: '1vh' }} height={200} />
          <Skeleton variant="rectangular" sx={{ mt: '1vh' }} height={300} />
        </Container>
      </BaseLayout>
    );
  }

  if (error || data === null) {
    return (
      <BaseLayout>
        <Container
          maxWidth={false}
          sx={{ px: 1, pt: { xs: '1vh', sm: '1vh', md: '2vh' } }}
        >
          <Alert severity="error">
            {error || 'Não foram encontrados dados'}
          </Alert>
        </Container>
      </BaseLayout>
    );
  }

  if (JSON.stringify(data) === '-10' || JSON.stringify(data) === '-1') {
    return (
      <BaseLayout>
        <Container
          maxWidth={false}
          sx={{ px: 1, pt: { xs: '1vh', sm: '1vh', md: '2vh' } }}
        >
          <Alert severity="error">{'Não há arquivos na pasta'}</Alert>
        </Container>
      </BaseLayout>
    );
  }

  return (
    <BaseLayout>
      <Container
        maxWidth={false}
        sx={{ px: 1, pt: { xs: '1vh', sm: '1vh', md: '2vh' } }}
      >
        <Typography variant="h3" align="center" sx={{ color: 'black' }}>
          O Dust identifica a presença de ataques de Port Scan na rede
        </Typography>
        <Divider />
        <Card variant="outlined" sx={{ mt: '2vh' }}>
          <Typography
            variant="h6"
            align="left"
            gutterBottom
            sx={{ padding: '1vh' }}
          >
            Uma rede neural artificial treinada é utilizada para identificar a
            presença de ataques de Port Scan nos pacotes da rede.
          </Typography>
          <Divider />
          <Typography
            variant="h6"
            align="left"
            gutterBottom
            sx={{ padding: '1vh' }}
          >
            São apenas três informações dos pacotes:{' '}
            <span style={{ color: 'red' }}>tamanho, direção e timestamp</span>
          </Typography>
          <Divider />
          <Typography
            variant="h6"
            align="left"
            gutterBottom
            sx={{ padding: '1vh' }}
          >
            Esse é um mecanismo que preserva a{' '}
            <span style={{ color: 'red' }}>privacidade</span> dos pacotes.
          </Typography>
        </Card>
        <Typography variant="h3" align="center" sx={{ color: 'black', mt: 1 }}>
          Descrição do Pré-processamento de PCAP
        </Typography>
        <Divider />
        <Card variant="outlined" sx={{ mt: '2vh', padding: '1vh' }}>
          <Typography variant="h5" align="left" sx={{ color: 'black' }}>
            <strong>Objetivo</strong>
          </Typography>
          <Typography variant="h6" align="left" gutterBottom>
            Extrair e analisar três características principais de pacotes de
            rede de um arquivo PCAP utilizando{' '}
            <span style={{ color: 'green' }}>tshark</span>: o tamanho do pacote,
            o timestamp e a direção do tráfego.
          </Typography>
          <Divider />

          <Typography variant="h5" align="left" sx={{ color: 'black' }}>
            <strong>Passos do Pré-processamento</strong>
          </Typography>
          <ol>
            <li>
              <Typography variant="h6" align="left">
                <strong>Leitura do Arquivo PCAP</strong>: Utilize o{' '}
                <span style={{ color: 'green' }}>tshark</span> para ler o
                arquivo PCAP. O <span style={{ color: 'green' }}>tshark</span> é
                uma ferramenta de linha de comando que faz parte do conjunto
                Wireshark e permite a análise de tráfego de rede.
              </Typography>
            </li>
            <li>
              <Typography variant="h6" align="left">
                <strong>Extração das Features</strong>:
                <ul>
                  <li>
                    <strong>Tamanho do Pacote</strong>: Utilize{' '}
                    <span style={{ color: 'green' }}>tshark</span> para extrair
                    o tamanho de cada pacote. A opção{' '}
                    <span style={{ color: 'green' }}>-e frame.len</span> pode
                    ser usada para isso.
                  </li>
                  <li>
                    <strong>Timestamp</strong>: O timestamp de cada pacote pode
                    ser extraído usando{' '}
                    <span style={{ color: 'green' }}>tshark</span> com a opção{' '}
                    <span style={{ color: 'green' }}>-e frame.time_epoch</span>.
                  </li>
                  <li>
                    Direção do Pacote: A direção do pacote pode ser determinada
                    com base nos endereços IP de origem e destino.{' '}
                    <span style={{ color: 'green' }}>tshark</span> pode ser
                    configurado para exibir os endereços IP usando -e{' '}
                    <span style={{ color: 'green' }}>ip.src</span> e -e{' '}
                    <span style={{ color: 'green' }}>ip.dst</span>.
                  </li>
                </ul>
              </Typography>
            </li>
            <li>
              <Typography variant="h6" align="left">
                <strong>Armazenamento dos Dados</strong>: Após extrair as
                características desejadas com{' '}
                <span style={{ color: 'green' }}>tshark</span>, os dados são
                armazenados em um formato adequado para análise posterior, como
                CSV, posteriormente manipulados por Python.
              </Typography>
            </li>
          </ol>
        </Card>

        <Typography
          variant="h3"
          align="center"
          sx={{ color: 'black', mt: '2vh' }}
        >
          Classes identificadas nos pacotes da rede
        </Typography>
        <Divider />

        <Grid container spacing={2}>
          <Grid item xs={12} sx={{ display: 'flex' }}>
            {[
              {
                color: styles.infoBox1,
                text: 'Ataque Portscan',
              },
              {
                color: styles.infoBox3,
                text: 'Dados',
              },
            ].map((info, index) => (
              <Grid
                item
                xs={12}
                sm={6}
                key={index}
                sx={{ display: 'flex', padding: '0 10px' }}
              >
                {' '}
                <Paper sx={{ ...styles.infoBox, ...info.color }}>
                  <Typography
                    variant="h6"
                    sx={{
                      fontSize: '1.5rem',
                      textAlign: 'center',
                    }}
                  >
                    {info.text}
                  </Typography>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </Grid>

        <Grid container spacing={2} mt={2}>
          <Grid
            item
            xs={12}
            sm={6}
            sx={{ maxWidth: { xs: '100%', sm: '45vw' } }}
          >
            <SampleDistributionGraph
              labels={data.labels_map}
              dataSizes={dataSizes}
              isDefense
            />
          </Grid>
          <Grid
            item
            xs={12}
            sm={6}
            container
            justifyContent="center"
            alignItems="center"
          >
            <Stack direction="column" spacing={2}>
              <Card variant="outlined" sx={{ mb: 2, mt: 4, p: 3 }}>
                <Box sx={{ p: 2 }}>
                  <Stack
                    direction="row"
                    justifyContent="space-evenly"
                    alignItems="center"
                    spacing={2}
                  >
                    <Typography variant="h5" component="div" fontWeight="bold">
                      Pacote de dados
                    </Typography>
                    <Typography
                      variant="h5"
                      component="div"
                      sx={{ color: '#1122bd' }}
                    >
                      {dataPercentage.toFixed(2)}%
                    </Typography>
                  </Stack>
                </Box>
              </Card>
              <Card variant="outlined" sx={{ mb: 4, p: 3 }}>
                <Box sx={{ p: 2 }}>
                  <Stack
                    direction="row"
                    justifyContent="space-evenly"
                    alignItems="center"
                    spacing={2}
                  >
                    <Typography variant="h5" component="div" fontWeight="bold">
                      Pacotes de ataque Portscan
                    </Typography>
                    <Typography
                      variant="h5"
                      component="div"
                      sx={{ color: '#ff0000' }}
                    >
                      {attackPercentage.toFixed(2)}%
                    </Typography>
                  </Stack>
                </Box>
              </Card>
            </Stack>
          </Grid>
        </Grid>
      </Container>
    </BaseLayout>
  );
}

export default DefenseModel;
