import React, { useContext } from 'react';
import { Container, Divider } from '@mui/material';
import ConfusionMatrixContainer from '../../../components/ConfusionMatrixContainer/ConfusionMatrixContainer';
import { AuthContext } from '../../../AuthContext';

const OriginalSamples: React.FC = () => {
  const { isUsingAggregatedDatabase } = useContext(AuthContext);

  return (
    <Container maxWidth={false} sx={{ px: 1, mt: 2 }}>
      <Divider />
      <ConfusionMatrixContainer
        dataType="original"
        source={isUsingAggregatedDatabase ? 'aggregated' : 'uploaded'}
      />
    </Container>
  );
};

export default OriginalSamples;
