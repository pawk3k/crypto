// render molstar-react molecule with no panes and no header
import React from 'react';


const MolStar = (props: any) => {
  return (
    <div>
      <Mol
        {...props}
        panes={[]}
        header={false}
      />
    </div>
  );
};