import React  from 'react';
import numeral from 'numeral';

export function DisplayCount(props) {
	return <span>{numeral(props.number).format("0a")}</span>
}
