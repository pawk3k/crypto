// Molstar molecule component for React
import React from 'react';
import {Mol} from './mol';
// ------------------------------------------------------------------
const Molstar = ({
  mol,  // molecule to render
    style, // style to apply to the molecule   
    ...props // other props to pass to the molecule
}) => {
    // console.log('Molstar:', mol, style, props);
    return (
        <div style={style}>
        <Mol
            mol={mol}
            style={{
            width: '100%',
            height: '100%',
            border: '1px solid black',
            borderRadius: '5px',
            ...style
            }}
            {...props}
        />
        </div>
    );
    };
