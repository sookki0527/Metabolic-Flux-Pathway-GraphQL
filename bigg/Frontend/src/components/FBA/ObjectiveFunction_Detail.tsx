import { gql, useQuery } from '@apollo/client';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ListGroup } from 'react-bootstrap';
import { useParams } from 'react-router-dom';
const OBJECTIVE_QUERY = gql`
 query ObjectiveFunctionPathways($name: String!) {
    pathwaysByObjective(objective : $name){
      id
      name
      pathwayLinks{
        reaction{
          id
          name
        }
      }
    }
}
`;

function ObjectiveFunctionDetailComponent(){
    const { label } = useParams<{ label: string }>();
    const objective = label;
   console.log("objective: "+ objective)
    const { loading, error, data } = useQuery(OBJECTIVE_QUERY, {
        variables: { name: objective || '' },
        skip: !objective,
    });
    const navigate = useNavigate();
    const handleSelect = (pathwayId: number) => {
      navigate(`/objectives/reactions/${pathwayId}`);
    };
    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error.message}</p>;

   return (
    <div>
      <h3>Select Objective Pathway for {objective}</h3>
      <ListGroup>
        {data.pathwaysByObjective.map((pathway: any) => (
          <ListGroup.Item key={pathway.id}
            action 
            onClick={() => handleSelect(pathway.id)}
            style={{ cursor: 'pointer' }}>
          {pathway.name}

          </ListGroup.Item>
        ))}
      </ListGroup>
    </div>
  );



}

export default ObjectiveFunctionDetailComponent