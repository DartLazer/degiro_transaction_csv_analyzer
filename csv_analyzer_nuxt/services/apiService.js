import axios from 'axios';

const { public: { apiAddress } } = useRuntimeConfig();
const customTimeout = 5000;

export const uploadCsv = async (selectedFile) => {
  const formData = new FormData();
  formData.append('csv_file', selectedFile, selectedFile.name);

  const config = {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: customTimeout,
  };

  try {
    const response = await axios.post(`http://${apiAddress}/calculate_multi_year_gain/`, formData, config);
    return { data: response.data, error: null };
  } catch (error) {
    let serverErrorMessage;

    if (error.response && error.response.data && error.response.data.error) {
      serverErrorMessage = error.response.data.error;
    } else if (error.code === 'ECONNABORTED') {
      serverErrorMessage = 'Request timed out';
    } else {
      serverErrorMessage = 'Error connecting to server';
    }

    return { data: null, error: serverErrorMessage };
  }
};
