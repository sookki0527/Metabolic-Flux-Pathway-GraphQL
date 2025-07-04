
import './App.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import ReactionComponent from './components/ReactionTable';
import client from './graphql/client';
import PathwayComponent from './components/PathwayTable'
import { ApolloProvider } from '@apollo/client/react';
import ObjectiveFunctionComponent from './components/FBA/ObjectiveFunction';
import ObjectiveFunctionDetailComponent from './components/FBA/ObjectiveFunction_Detail';
import ObjectiveFunctionDetailReactionComponent from './components/FBA/ObjectiveFunction_Detail_reaction';
import SelectedObjectiveFunctionComponent from './components/FBA/SelectedObjectiveFunction';

import NetworkComponent from './components/Network/Network';
import HomeComponent from './pages/Home';
function App() {


    return (
    <ApolloProvider client={client}>
     <Router>
        <Routes>
          <Route path = "/" element = {<HomeComponent />} />
          <Route path="/pathways" element={<PathwayComponent />} />
          <Route path="/reactions/:id" element={<ReactionComponent />} />
          <Route path ="/objective" element = {<ObjectiveFunctionComponent />} />
          <Route path ="/objectives/:label" element = {<ObjectiveFunctionDetailComponent />} />
          <Route path = "/objectives/reactions/:pathwayId" element = {<ObjectiveFunctionDetailReactionComponent />}/>
          <Route path = "/objective-selected/:entryId" element = {<SelectedObjectiveFunctionComponent />} />
          <Route path = "/network/compute" element={<NetworkComponent />} />
        </Routes>
      </Router>
    </ApolloProvider>
  );
}

export default App
