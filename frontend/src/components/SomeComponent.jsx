// components/SomeComponent.jsx
import { useNavigate } from 'react-router-dom';

function SomeComponent() {
  const navigate = useNavigate();

  const handleRedirect = () => {
    // Redirects to the Hive Management page
    navigate('/hive-management');
  };

  return (
    <button onClick={handleRedirect}>
      Go to Hive Management
    </button>
  );
}

export default SomeComponent;
