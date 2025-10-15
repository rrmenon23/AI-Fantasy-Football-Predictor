import React from 'react'


type Props = { name: string; team: string; position: string; points: number }


export default function PredictionCard({name, team, position, points}: Props){
return (
<div className="border rounded p-4 bg-white">
<div className="flex items-center justify-between">
<div>
<div className="text-lg font-semibold">{name}</div>
<div className="text-xs text-gray-500">{team} · {position}</div>
</div>
<div className="text-2xl font-bold">{points.toFixed(2)}<span className="text-sm font-normal text-gray-500"> pts</span></div>
</div>
</div>
)
}