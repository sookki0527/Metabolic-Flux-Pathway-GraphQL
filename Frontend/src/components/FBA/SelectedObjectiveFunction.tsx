import { gql, useQuery, useMutation } from '@apollo/client';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ListGroup,  Button, Card } from 'react-bootstrap';
import { useParams } from 'react-router-dom';
interface FluxLink {
  reaction?: {
    name: string;
  };
}

interface FluxType {
  value: number;
  fluxLinks: FluxLink[];
}

interface PathSegment {
  from_: number;
  to_: number;
  reactionId: number;
}
interface FluxResultType {
  objectiveFluxReactionid : number;
  objectiveFluxValue: number;
  topFluxes: FluxType[];
  totalFlux: number;
  nonZeroFluxCount: number;
  candidateSourceMetabolites: string[];
  fluxes: FluxType[];
  sourceMetabolite: string;
  segments: PathSegment[];
}

const FBA_MUTATION = gql`
  mutation RunFBA($entryId: String!) {
    fluxResult(entryId: $entryId){
      objectiveFluxReactionid
      objectiveFluxValue
      topFluxes{
        value
        fluxLinks{
          fluxId
          reactionId
          reaction{
            name
          }
        }
      }
      totalFlux
      nonZeroFluxCount
      fluxes{
        id
        value
        fluxLinks{
          fluxId
          reactionId
          reaction{
            name
            entryId
          }
        }
      }
      sourceMetabolite
      segments{
        from_,
        to_,
        reactionId
        reactionName
      }
    }
  }
`;
const OBJECTIVE_QUERY = gql`
 query ReactionByEntry($entryId: String!) {
   reactionByEntryId(entryId: $entryId){
        name
        entryId

   }
}
`;
function SelectedObjectiveFunctionComponent() {

    const { entryId } = useParams<{ entryId: string }>();
    const [fbaResult, setFbaResult] = useState<FluxResultType | null>(null);
    const [runFba, { loading: loading1, error: error1, data: data1 }] = useMutation(FBA_MUTATION);
    const { loading: loading2, error: error2, data: data2 }  = useQuery(OBJECTIVE_QUERY, {
            variables: { entryId: entryId || '' },
    });
    const navigate = useNavigate();
    useEffect(() => {
      if (entryId) {
        runFba({ variables: { entryId } }).then((res) => {
          setFbaResult(res.data.fluxResult);
        });
      }
    }, [entryId]);

    const handleSelect = () => {
      navigate(`/network/compute`,{
         state: {
          segments: fbaResult?.segments
         }
      });
    };
    if (loading1 || loading2 ) return <p>Computing FBA...</p>;
    if (error1 || error2) return <p>Error: {error1?.message || error2?.message}</p>;

    const objectiveReaction = data2?.reactionByEntryId;
   
    return (
    <div>
      <h3>FBA Results</h3>
       <Card className="h-100 shadow-sm">
            <Card.Body>
                <ListGroup>
                  <ListGroup.Item>
                    <strong> Flux value of {objectiveReaction?.name} :</strong> {" "}
                    {fbaResult?.objectiveFluxValue}
                  </ListGroup.Item>
                <ListGroup.Item>
                  <strong>Top 10 fluxes:</strong>
                  <ol>
                    {fbaResult?.topFluxes.map((flux: any, idx: number) => (
                      <li key={idx}>
                        {flux.fluxLinks?.[0]?.reaction?.name || "N/A"}: {flux.value}
                      </li>
                    ))}
                  </ol>
                </ListGroup.Item>
                  <ListGroup.Item>
                    Non-Zero Flux Count: {fbaResult?.nonZeroFluxCount}
                  </ListGroup.Item>
                  <ListGroup.Item>
                     Total Flux: {fbaResult?.totalFlux}
                  </ListGroup.Item>
                  <ListGroup.Item>
                    Source Metabolite: {fbaResult?.sourceMetabolite} 
                  </ListGroup.Item>
                </ListGroup>
              
            </Card.Body>
          </Card>
         <Button variant="outline-primary" size="sm" 
            onClick={() => handleSelect()}
            style={{ cursor: 'pointer' }}> Network Compute</Button>
    </div>
  );
}

export default SelectedObjectiveFunctionComponent