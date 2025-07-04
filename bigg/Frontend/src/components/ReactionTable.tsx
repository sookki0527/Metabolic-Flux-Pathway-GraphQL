import { gql, useQuery } from '@apollo/client';
import { useState } from 'react';
import { Card, Table, Row, Col } from 'react-bootstrap';
import { useParams } from 'react-router-dom';

const REACTION_QUERY = gql`
 query ReactionPathways($pathwayId: Int!) {
  reactionsByPathway(pathwayId: $pathwayId) {
    name
    equation
  }
}
`;

const PATHWAY_QUERY = gql`
 query GetPathway($pathwayId: Int!) {
  pathway(pathwayId: $pathwayId) {
    name
  }
}
`;

function ReactionComponent(){
    const { id } = useParams();
    const pathwayId = Number(id); 

    const { loading: loading1, error: error1, data: data1 } = useQuery(REACTION_QUERY, {
      variables: { pathwayId },
    });

    // 두 번째 쿼리: pathway 이름
    const { loading: loading2, error: error2, data: data2 } = useQuery(PATHWAY_QUERY, {
      variables: { pathwayId },
    });

    if (loading1 || loading2) return <p>Loading...</p>;
    if (error1 || error2) return <p>Error: {error1?.message || error2?.message}</p>;


    return (
    <div>
      <h3>Reactions for Pathway</h3>
       <Card className="h-100 shadow-sm">
            <Card.Body>
              <Card.Title>{data2.pathway.name}</Card.Title>
              <Table striped bordered hover size="sm">
                <thead>
                  <tr>
                    <th> Reaction</th>
                    <th> Equation </th>
                  </tr>
                </thead>
                <tbody>
                  {data1.reactionsByPathway.map((reaction: any, idx: number) => (
                   <tr key={idx}>
                      <td>{reaction.name}</td>
                      <td>{reaction.equation}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </Card.Body>
          </Card>
      
    </div>
  );
}
export default ReactionComponent