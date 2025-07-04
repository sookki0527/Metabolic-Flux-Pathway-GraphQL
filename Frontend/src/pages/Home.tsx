import { useNavigate } from 'react-router-dom';
import { Card, Button, Container, Row, Col } from 'react-bootstrap';

function HomeComponent() {
  const navigate = useNavigate();

  return (
    <Container className="mt-4">
      <Row>
        <Col md={6}>
          <Card>
            <Card.Body>
              <Card.Title>Metabolic Flux Balance Analysis</Card.Title>
              <Card.Subtitle className="mb-2 text-muted">
                Select Objective Pathway & Reactions
              </Card.Subtitle>
              <Card.Text>
                Computes the fluxes of each reaction using FBA.
              </Card.Text>
              
            </Card.Body>
          </Card>
        </Col>

        <Col md={6}>
          <Card>
            <Card.Body>
              <Card.Title>Shortest Path from Computed Flux</Card.Title>
              <Card.Subtitle className="mb-2 text-muted">Using Dijkstra</Card.Subtitle>
              <Card.Text>
                Visualize the shortest path between metabolites.
              </Card.Text>
     
            </Card.Body>
          </Card>
        </Col>
      </Row>
<Card className="p-3">
  <div
    style={{
      display: 'flex',
      justifyContent: 'center',   // 수평 가운데 정렬
      alignItems: 'center',       // 수직 정렬 (버튼 높이 같으면 영향 적음)
      gap: '12px'
    }}
  >
    <Button
      variant="outline-primary"
      style={{ width: '150px', height: '40px' }}
      onClick={() => navigate('/objective')}
    >
      FBA Start
    </Button>

    <Button
      variant="outline-primary"
      style={{ width: '150px', height: '40px' }}
      onClick={() => navigate('/pathways')}
    >
      Pathways
    </Button>
  </div>
</Card>

    
    </Container>
  );
}

export default HomeComponent;
