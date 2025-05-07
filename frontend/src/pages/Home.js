import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import {
  Box,
  Typography,
  Paper,
  Button,
  CircularProgress,
  Grid,
  Card,
  CardContent,
  CardMedia,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import axios from 'axios';

const UploadBox = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(4),
  textAlign: 'center',
  cursor: 'pointer',
  border: `2px dashed ${theme.palette.primary.main}`,
  backgroundColor: theme.palette.background.paper,
  '&:hover': {
    backgroundColor: theme.palette.action.hover,
  },
}));

const ResultCard = styled(Card)(({ theme }) => ({
  marginTop: theme.spacing(4),
  maxWidth: 600,
  margin: '0 auto',
}));

function Home() {
  const [image, setImage] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const onDrop = (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      setImage(URL.createObjectURL(file));
      setPrediction(null);
      setError(null);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png'],
    },
    maxFiles: 1,
  });

  const handlePredict = async () => {
    if (!image) return;

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      const response = await fetch(image);
      const blob = await response.blob();
      formData.append('image', blob, 'image.jpg');

      const result = await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setPrediction(result.data);
    } catch (err) {
      setError('Error predicting the disease. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ textAlign: 'center', mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          Tea Leaf Disease Detection
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Upload an image of a tea leaf to detect potential diseases
        </Typography>
      </Box>

      <UploadBox {...getRootProps()}>
        <input {...getInputProps()} />
        <CloudUploadIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
        <Typography variant="h6" gutterBottom>
          {isDragActive
            ? 'Drop the image here'
            : 'Drag and drop an image here, or click to select'}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Supported formats: JPG, JPEG, PNG
        </Typography>
      </UploadBox>

      {image && (
        <Box sx={{ mt: 4, textAlign: 'center' }}>
          <img
            src={image}
            alt="Uploaded tea leaf"
            style={{ maxWidth: '100%', maxHeight: '400px', objectFit: 'contain' }}
          />
          <Button
            variant="contained"
            color="primary"
            onClick={handlePredict}
            disabled={loading}
            sx={{ mt: 2 }}
          >
            {loading ? <CircularProgress size={24} /> : 'Predict Disease'}
          </Button>
        </Box>
      )}

      {error && (
        <Typography color="error" sx={{ mt: 2, textAlign: 'center' }}>
          {error}
        </Typography>
      )}

      {prediction && (
        <ResultCard>
          <CardContent>
            <Typography variant="h5" component="h2" gutterBottom>
              Prediction Result
            </Typography>
            <Typography variant="body1" gutterBottom>
              Disease: {prediction.data.disease}
            </Typography>
            <Typography variant="body1" gutterBottom>
              Confidence: {prediction.data.confidence}%
            </Typography>
            {prediction.data.tips && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Recommended Actions:
                </Typography>
                <ul>
                  {prediction.data.tips.map((tip, index) => (
                    <li key={index}>
                      <Typography variant="body2">{tip}</Typography>
                    </li>
                  ))}
                </ul>
              </Box>
            )}
          </CardContent>
        </ResultCard>
      )}
    </Container>
  );
}

export default Home; 