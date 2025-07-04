import { gql, useQuery } from '@apollo/client';
import { useState } from 'react';
import { ListGroup } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';


  const OBJECTIVE_OPTIONS = [
    "Biomass Production", "ATP Maintenance and Production" , "Amino Acid Production",
    "Organic Acid Production", "Glucose Uptake and Sugar Metabolism"
  ];
function ObjectiveFunctionComponent() {

    const navigate = useNavigate();

    const handleSelect = (label: string) => {
      const formattedLabel = label.toLowerCase().replace(/ /g, '-').replace(/\//g, '');
      // console.log(label);
      navigate(`/objectives/${label}`);
    };

  return (
    <div>
      <h3>Select Objective Function For FBA</h3>
       <ListGroup>
        {OBJECTIVE_OPTIONS.map((label, idx) => (
          <ListGroup.Item 
            key={idx} 
            action 
            onClick={() => handleSelect(label)}
            style={{ cursor: 'pointer' }}
          >
            {label}
          </ListGroup.Item>
        ))}
      </ListGroup>
    </div>
  );

}
export default ObjectiveFunctionComponent