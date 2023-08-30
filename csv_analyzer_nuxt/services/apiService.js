import axios from 'axios';

// Address of the API service, localhost:8000 when running locally in docker
const apiAddress = 'localhost:8000'

// Time to wait for response on the server
const customTimeout = 5000

export const uploadCsv = async (selectedFile) => {
  const formData = new FormData();
  formData.append('csv_file', selectedFile, selectedFile.name);

  try {
    const response = await axios.post(`http://${apiAddress}/calculate_multi_year_gain/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: customTimeout,
    });
    return { data: response.data, error: null };
  } catch (error) {
    let serverErrorMessage;

    if (error.response && error.response.data && error.response.data.error) {
      // Server-side error
      serverErrorMessage = error.response.data.error;
    } else if (error.code === 'ECONNABORTED') {
      // Timeout error
      serverErrorMessage = 'Request timed out';
    } else {
      // Network error or problem connecting to the server
      serverErrorMessage = 'Error connecting to server';
    }

    return { data: null, error: serverErrorMessage };
  }
};