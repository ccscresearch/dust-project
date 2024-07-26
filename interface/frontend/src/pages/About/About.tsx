import React from 'react';
import { Link } from 'react-router-dom';
import {
  Container,
  Typography,
  Grid,
  Paper,
  Box,
  Divider,
} from '@mui/material';

import BaseLayout from '../../components/BaseLayout/BaseLayout';
import { styles } from './style';

const AdversarialHeader: React.FC = () => (
  <>
    <Typography variant="h3" sx={styles.sectionHeader}>
      Bem vindo ao Dust
    </Typography>
    <Divider />
    <Grid container spacing={2} sx={{ margin: '20px 0' }}>
      {[
        {
          color: styles.infoBox1,
          text: 'O Dust é um estudo de caso que atua na identificação de ataques, sem violar a privacidade dos dispositivos. Inicialmente aplicado em dois contextos distintos.',
        },
        {
          color: styles.infoBox2,
          text: (
            <>
              Modelos de aprendizagem de máquina fazem a identificação usando
              apenas a{' '}
              <Box component="span" sx={styles.boldText}>
                direção dos pacotes, tamanhos e tempos de chegada
              </Box>
              .
            </>
          ),
        },
        {
          color: styles.infoBox3,
          text: 'São geradas e aplicadas amostras adversariais que confrontam o modelo de defesa.',
        },
      ].map((info, index) => (
        <Grid
          item
          xs={12}
          sm={4}
          key={index}
          sx={{ display: 'flex', padding: '0 10px' }}
        >
          <Paper sx={{ ...styles.infoBox, ...info.color }}>
            <Typography
              variant="body1"
              sx={{
                fontSize: '1.5rem',
                color: '#fff',
                textAlign: 'center',
              }}
            >
              {info.text}
            </Typography>
          </Paper>
        </Grid>
      ))}
    </Grid>
  </>
);

const Scenarios: React.FC = () => (
  <>
    <Typography variant="h3" sx={styles.sectionHeader}>
      Em quais cenários o Dust foi aplicado?
    </Typography>
    <Divider />
    <Paper sx={styles.scenarioBox}>
      <Typography sx={{ fontSize: '1.5rem', mb: 2 }}>
        O Dust foi aplicado em bases de dados publicamente disponíveis.
      </Typography>
      <Divider />
      <Typography sx={{ fontSize: '1.5rem', my: 2 }}>
        A base pública{' '}
        <Box component="span" sx={styles.boldText}>
          Discrimation-Flow Database
        </Box>{' '}
        foi utilizada para o estudo com as amostras adversáriais.
      </Typography>
      <Divider />
      <Typography sx={{ fontSize: '1.5rem', mt: 2 }}>
        As bases públicas:{' '}
        <Box component="span" sx={styles.boldText}>
          Cenário experimental / Testbed, Intrusion Detection Evaluation
          Dataset, Multistep Cyber Attack Dataset, Edge-IIOTSET- Dataset of
          Porscanning Attacks on emulation testbed e hardware-in-the-loop
        </Box>{' '}
        foram utilizadas para o estudo do modelo de defesa.
      </Typography>
    </Paper>
  </>
);

const HowTo: React.FC = () => (
  <>
    <Typography variant="h3" sx={styles.sectionHeader}>
      Como usar o Dust?
    </Typography>
    <Divider />
    <Paper sx={styles.howToBox}>
      <Link to="/database">
        1 - Abra a aba &apos;Base de dados&apos;, e selecione uma base.
      </Link>
    </Paper>
    <Paper sx={styles.howToBox}>
      <Link to="/database">
        2 - Caso tenha selecionado uma base diferente das investigadas em
        laboratório, aguarde o processamento.
      </Link>
    </Paper>
    <Paper sx={styles.howToBox}>
      <Link to="/adversarial">
        3 - Veja o desempenho isolado das amostras adversarias na aba
        &apos;Amostras adversarias&apos;.
      </Link>
    </Paper>
    <Paper sx={styles.howToBox}>
      <Link to="/defense">
        4 - Confira o resultado da análise do modelo de defesa na aba
        &apos;Modelo de defesa&apos;.
      </Link>
    </Paper>
  </>
);

const About: React.FC = () => (
  <BaseLayout>
    <Container
      maxWidth={false}
      sx={{ px: 1, pt: { xs: '1vh', sm: '1vh', md: '2vh' } }}
    >
      <AdversarialHeader />
      <Divider />
      <Scenarios />
      <Divider />
      <HowTo />
    </Container>
  </BaseLayout>
);

export default About;
