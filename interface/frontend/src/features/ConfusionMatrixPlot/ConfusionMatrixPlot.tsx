import React from 'react';
import Plot from 'react-plotly.js';
import { Data, Layout, Annotations } from 'plotly.js';
import { Box, Card, Grid, Stack, Typography } from '@mui/material';

interface ConfusionMatrixPlotProps {
  isOriginal: boolean;
  title: string;
  accuracy: number;
  matrixData: number[][];
  labels: { [key: string]: string };
  originalAccuracy?: number;
}

const ConfusionMatrixPlot: React.FC<ConfusionMatrixPlotProps> = ({
  isOriginal,
  title,
  accuracy,
  matrixData,
  labels,
  originalAccuracy,
}) => {
  const sortedClasses = Object.keys(labels).sort(
    (a, b) => Number(a) - Number(b),
  );
  const reversedClasses = [...sortedClasses].reverse();

  // Dados para o gráfico de calor
  const heatmapData: Data[] = [
    {
      z: matrixData,
      x: reversedClasses,
      y: sortedClasses,
      text: matrixData.flatMap((row) =>
        row.map((value) => `${value.toFixed(2)}%`),
      ),
      type: 'heatmap',
      colorscale: 'Portland',
      showscale: true,
    },
  ];

  // Layout do gráfico
  const layout: Partial<Layout> = {
    title,
    xaxis: {
      title: 'Rótulo Predito',
      side: 'top',
    },
    yaxis: {
      title: 'Rótulo Verdadeiro',
      autorange: 'reversed', // Inverte o eixo Y para correspondência correta
    },
    annotations: generateAnnotations(
      matrixData,
      sortedClasses,
      reversedClasses,
    ),
  };

  // Função para gerar anotações no gráfico
  function generateAnnotations(
    matrix: number[][],
    classesAscending: string[],
    classesDescending: string[],
  ): Annotations[] {
    return matrix.flatMap((row, i) =>
      row.map((value, j) => ({
        xref: 'x',
        yref: 'y',
        x: classesDescending[j],
        y: classesAscending[i],
        text: `${value.toFixed(2)}%`,
        font: {
          family: 'Arial',
          size: 12,
          color: 'rgb(255, 255, 255)',
        },
        showarrow: false,
      })),
    ) as Annotations[];
  }

  return (
    <Box
      display="flex"
      flexDirection="column"
      justifyContent="center"
      alignItems="center"
    >
      {/* Gráfico Plotly */}
      <Plot data={heatmapData} layout={layout} />

      {/* Cartões de Precisão */}
      <Grid container spacing={2} sx={{ mt: 2, width: '50%' }}>
        {!isOriginal && (
          <Grid item xs={12}>
            <Card variant="outlined">
              <Box sx={{ p: 2 }}>
                <Stack
                  direction="row"
                  justifyContent="space-between"
                  alignItems="center"
                >
                  <Typography variant="h5" component="div" fontWeight="bold">
                    Precisão com dados reais
                  </Typography>
                  <Typography
                    variant="h5"
                    component="div"
                    sx={{ color: '#1122bd' }}
                  >
                    {originalAccuracy?.toFixed(2)}%
                  </Typography>
                </Stack>
              </Box>
            </Card>
          </Grid>
        )}
        <Grid item xs={12}>
          <Card variant="outlined">
            <Box sx={{ p: 2 }}>
              <Stack
                direction="row"
                justifyContent="space-between"
                alignItems="center"
              >
                <Typography variant="h5" component="div" fontWeight="bold">
                  {isOriginal
                    ? 'Precisão'
                    : 'Precisão com Amostras Adversárias'}
                </Typography>
                <Typography
                  variant="h5"
                  component="div"
                  sx={{ color: '#ff0000' }}
                >
                  {accuracy.toFixed(2)}%
                </Typography>
              </Stack>
            </Box>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ConfusionMatrixPlot;
