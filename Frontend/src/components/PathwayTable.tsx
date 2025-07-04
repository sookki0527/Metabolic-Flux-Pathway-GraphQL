
import { gql, useQuery } from '@apollo/client';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { Card, Table, Row, Col } from 'react-bootstrap';

const PATHWAY_QUERY = gql`
  query {
    pathways{
        id
        name
        category
    }
  }
`;

function PathwayComponent() {
  const { loading, error, data} = useQuery(PATHWAY_QUERY);
  //const [selectedPathways, setSelectedPathways] = useState<Set<string>>(new Set());
  const navigate = useNavigate();

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;
  const grouped: Record<string, { id: number, name: string }[]> = {};

  data.pathways.forEach((pathway: {  id: number;  name: string; category: string }) => {
    if (!grouped[pathway.category]) {
      grouped[pathway.category] = [];
    }
    grouped[pathway.category].push({   
      id: pathway.id, name: pathway.name });
  });
  return (
  <div>
    <Row>
      {Object.entries(grouped).map(([category, pathways]) => (
        <Col key={category} md={4} className="mb-4">
          <Card className="h-100 shadow-sm">
            <Card.Body>
              <Card.Title>{category}</Card.Title>
              <Table striped bordered hover size="sm">
                <thead>
                  <tr>
                    <th>Pathway</th>
                  </tr>
                </thead>
                <tbody>
                  {pathways.map((pathway, idx) => (
                   <tr
                      key={idx}
                      style={{ cursor: 'pointer' }}
                      onClick={() => navigate(`/reactions/${pathway.id}`)}
                    >
                      <td>{pathway.name}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
        </Col>
      ))}
    </Row>
  </div>
);
}

export default PathwayComponent