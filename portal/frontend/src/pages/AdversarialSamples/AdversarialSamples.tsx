import React, { useContext } from 'react';
import { Container, Typography, Divider, Card } from '@mui/material';
import BaseLayout from '../../components/BaseLayout/BaseLayout';
import ConfusionMatrixContainer from '../../components/ConfusionMatrixContainer/ConfusionMatrixContainer';
import { AuthContext } from '../../AuthContext';
import { styles } from './style';

const AdversarialSamples: React.FC = () => {
  const { isUsingAggregatedDatabase } = useContext(AuthContext);

  return (
    <BaseLayout>
      <Container maxWidth={false} sx={styles.container}>
        <Typography variant="h3" sx={styles.title}>
          O que são e como o Dust as aplica?
        </Typography>
        <Divider sx={{ marginBottom: '2rem' }} />

        <Card variant="outlined" sx={styles.card}>
          <Typography variant="h6" gutterBottom>
            Amostras adversárias são registros gerados que parecem similares aos
            dados reais, mas que são usados para enganar modelos de aprendizagem
            de máquina.
          </Typography>
          <Divider sx={{ margin: '1rem 0' }} />
          <Typography variant="h6" gutterBottom>
            As amostras adversárias são utilizadas para avaliar o desempenho do
            modelo de defesa proposto nesse contexto. Essa página mostra o
            desempenho das amostras em uma rede neural simples, mas o real
            mecanismo de defesa é apresentado na aba &apos;Modelo de
            defesa&apos;.
          </Typography>
        </Card>

        <ConfusionMatrixContainer
          dataType={isUsingAggregatedDatabase ? 'adversarial' : 'adversarial'}
          source={isUsingAggregatedDatabase ? 'aggregated' : 'uploaded'}
        />
      </Container>
    </BaseLayout>
  );
};

export default AdversarialSamples;
