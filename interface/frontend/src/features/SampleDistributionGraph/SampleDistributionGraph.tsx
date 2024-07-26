/* eslint-disable react/react-in-jsx-scope */
import { Box, Container, Grid, Typography } from '@mui/material';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);

interface IProps {
  instances?: number[][];
  labels: { [key: string]: string };
  dataSizes: { dataset: number; [key: string]: number } | undefined;
  isDefense?: boolean;
}

const SampleDistributionGraph = ({ labels, dataSizes, isDefense }: IProps) => {
  const columnSums = Object.keys(labels).map((key) => dataSizes?.[key] ?? 0);

  const totalSum = dataSizes?.dataset ?? 0;

  const data = {
    labels: Object.keys(labels).map((key) => labels[key]),
    datasets: [
      {
        label: 'Distribuição',
        data: columnSums,
        backgroundColor: [
          '#009E73',
          '#ff0000',
          '#0072BB',
          '#CC79A7',
          '#F0E442',
          '#56B4E9',
          '#D55E00',
          '#CC79A7',
          '#29268b',
          '#000000',
          '#5abc21',
          '#8f1f6d',
          '#def816',
        ],
      },
    ],
  };

  const options = {
    plugins: {
      legend: {
        position: 'top' as const,
        labels: {
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          generateLabels: (chart: any) => {
            return chart.data.labels.map((label: string, index: number) => {
              const value = columnSums[index];
              const percentage = ((value / totalSum) * 100).toFixed(2);
              return {
                text: `${label}: (${percentage}%)`,
                fillStyle: data.datasets[0].backgroundColor[index],
              };
            });
          },
        },
      },
    },
  };

  return (
    <Box
      display="flex"
      flexDirection="column"
      justifyContent="center"
      alignItems="center"
      sx={{ mt: 10, height: '75%', width: '75%' }}
    >
      <Container>
        <Typography
          variant="h6"
          align="center"
          gutterBottom
          sx={{ color: 'black' }}
        >
          {isDefense ? 'Distribuição dos pacotes' : 'Distribuição dos dados'}
        </Typography>
        <Pie data={data} options={options} />
        <Grid container spacing={2} sx={{ mt: 2 }}>
          {Object.keys(labels).map((key, index) => (
            <Grid item xs={12} sm={6} key={index}>
              <Box
                sx={{
                  mb: 1,
                  backgroundColor: data.datasets[0].backgroundColor[index],
                  border: '2px solid black',
                  borderRadius: '5px',
                  p: 1,
                }}
              >
                <Typography
                  variant="body1"
                  sx={{ color: '#fff' }}
                  fontWeight="bold"
                >
                  {labels[key]}: {columnSums[index]}
                </Typography>
              </Box>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

export default SampleDistributionGraph;
