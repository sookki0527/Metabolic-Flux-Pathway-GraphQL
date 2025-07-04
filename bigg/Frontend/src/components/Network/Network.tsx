
import { useLocation, useNavigate } from 'react-router-dom';
import {Button} from 'react-bootstrap'



function NetworkComponent(){
    const navigate = useNavigate();
    const { state } = useLocation();
    const segments = state?.segments || [];
    const handleSelect = () => {
      navigate(`/`);
    };
  return (
      <div>
      <h4>Shortest Flux Path </h4>
      <ul>
        {segments.map((seg: any, idx: number) => (
          <li key={idx}>
            {seg.from_} → {seg.to_} (reaction <strong>{seg.reactionName}</strong>)
          </li>
        ))}
      </ul>

          <Button variant="outline-primary" size="sm" 
            onClick={() => handleSelect()}
            style={{ cursor: 'pointer' }}>Go back to Home</Button>
    </div>
  );
}
export default NetworkComponent