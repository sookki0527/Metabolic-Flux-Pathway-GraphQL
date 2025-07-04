import { gql, useQuery } from '@apollo/client';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ListGroup,  Button , Row, Col} from 'react-bootstrap';
import { useParams } from 'react-router-dom';
const OBJECTIVE_QUERY = gql`
 query ReactionPathways($pathwayId: Int!) {
   reactionsByPathway(pathwayId: $pathwayId){
        name
        entryId

   }
}
`;
const PATHWAY_QUERY = gql`
 query PathwayById($pathwayId: Int!) {
    pathway(pathwayId: $pathwayId){
        id
        name
   }
}
`;
function ObjectiveFunctionDetailReactionComponent(){
    const { pathwayId } = useParams();
    const id = parseInt(pathwayId || '0', 10);
    const { loading: loading1, error: error1, data: data1 }  = useQuery(OBJECTIVE_QUERY, {
        variables: { pathwayId: id || '' },
    });

    const { loading: loading2, error: error2, data: data2 } = useQuery (PATHWAY_QUERY, {
        variables: { pathwayId: id || ''}
        
    });

    const navigate = useNavigate();
    const handleSelect = (entryId: string) => {
      navigate(`/objective-selected/${entryId}`);
    };
    if (loading1 || loading2) return <p>Loading Reactions...</p>;
    if (error1 || error2) return <p>Error: {error1?.message || error2?.message}</p>;

   return (
    <div>
      <h3>Select Objective Reaction for {data2.pathway.name}</h3>
      <ListGroup>
        {data1.reactionsByPathway.map((reaction: any) => (
    <ListGroup.Item key={reaction.id}>
      <Row className="align-items-center">
        <Col xs={8}>{reaction.name}</Col>
        <Col xs="auto">
          <Button
            variant="outline-primary"
            size="sm"
            onClick={() => handleSelect(reaction.entryId)}
          >
            Select
          </Button>
        </Col>
      </Row>
    </ListGroup.Item>
  ))}
      </ListGroup>
    </div>
  );



}

export default ObjectiveFunctionDetailReactionComponent