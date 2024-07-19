export const styles = {
  infoBox: {
    backgroundColor: 'rgba(248, 248, 248, 0.8)',
    color: 'white',
    padding: '20px',
    border: '3px solid #0f055a',
    margin: '10px 0',
    borderRadius: '8px',
    boxShadow: '3px 3px 5px rgba(0, 0, 0, 0.2)',
    transition: 'transform 0.2s ease',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    flexGrow: 1,
    '&:hover': {
      transform: 'translateY(-2px)',
    },
  },
  infoBox1: {
    backgroundColor: '#c94f4f',
  },
  infoBox2: {
    backgroundColor: '#3fa3ca',
  },
  infoBox3: {
    backgroundColor: '#523fca',
  },
  sectionHeader: {
    textAlign: 'center',
    color: 'black',
    margin: '1vh 0',
  },
  scenarioBox: {
    backgroundColor: '#a8eaba',
    padding: '25px',
    border: '3px solid #0f055a',
    margin: '15px 0',
    borderRadius: '8px',
    boxShadow: '3px 3px 5px rgba(0, 0, 0, 0.2)',
    transition: 'transform 0.2s ease',
    '&:hover': {
      transform: 'translateY(-2px)',
    },
  },
  howToBox: {
    backgroundColor: '#aaa8ea',
    fontSize: '1.5rem',
    padding: '15px',
    border: '3px solid #0f055a',
    margin: '5px',
    borderRadius: '8px',
    boxShadow: '3px 3px 5px rgba(0, 0, 0, 0.2)',
    transition: 'transform 0.2s ease',
    '&:hover': {
      transform: 'translateY(-2px)',
    },
  },
  link: {
    color: '#0f055a',
    textDecoration: 'none',
    '&:hover': {
      textDecoration: 'underline',
    },
  },
  boldText: {
    fontWeight: 700,
  },
};
