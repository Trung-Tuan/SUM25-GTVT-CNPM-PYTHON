import react, { use, useEffect, useState } from 'react';

function App() {
  cosnt[data, setData] = useState({});
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await fetch(''); // url 
      const jsonData = await response.json(); // 
      setData(jsonData);
    } catch (error) {
      console.error('Error', error);
    }
  };

  return (
    <div className="App">

    </div>
  );
}

export default App;
