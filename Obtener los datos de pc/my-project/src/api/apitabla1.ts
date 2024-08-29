export const getSystemInfo = async () => {
  try {
    const response = await fetch(`http://localhost:5000/api/system_info`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("There was an error fetching the system info: ", error);
    return null;
  }
};
