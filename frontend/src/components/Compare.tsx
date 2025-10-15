import React, { useState } from 'react'
import { compare } from '../lib/api'
import PlayerSearch from './PlayerSearch'
import PredictionCard from './PredictionCard'
type Scoring = 'ppr' | 'half_ppr'

export default function Compare(){
    const [left, setLeft] = useState<any|null>(null)
    const [right, setRight] = useState<any|null>(null)
    const [week, setWeek] = useState<number>(5)
    const [season, setSeason] = useState<number>(2025)
    const [scoring, setScoring] = useState<Scoring>('ppr')
    const [resp, setResp] = useState<any>(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState<string|undefined>()


    const onSubmit = async () => {
        if(!left || !right) return
        try{
            setLoading(true)
            setError(undefined)
            const players = [left.player_id, right.player_id]
            const r = await compare({ players, season, week, scoring })
            setResp(r.data)
        }catch(e:any){
            setError(e?.message || 'Request failed')
        }finally{
            setLoading(false)
        }
    }


return (
        <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <PlayerSearch label="Player A" onSelect={setLeft} />
                <PlayerSearch label="Player B" onSelect={setRight} />
            </div>
            <div className="flex items-center gap-3">
                <label className="text-sm">Week</label>
                <input className="border rounded px-2 py-1 w-20" type="number" value={week} onChange={e=>setWeek(parseInt(e.target.value))} />
                <label className="text-sm ml-3">Scoring</label>
                <select className="border rounded px-2 py-1" value={scoring} onChange={e=>setScoring(e.target.value as Scoring)}>
                    <option value="ppr">Full PPR</option>
                    <option value="half_ppr">Half PPR</option>
                </select>
                <button onClick={onSubmit} disabled={!left || !right || loading}
                    className="ml-auto bg-black text-white px-3 py-2 rounded disabled:opacity-50">
                    {loading? 'Computing…' : 'Compare'}
                </button>
            </div>
            {error && <div className="text-red-600 text-sm">{error}</div>}
            {resp && (
                <div className="space-y-4">
                    <div className="p-3 border rounded bg-white">
                        <div className="font-medium">{resp.recommendation} <span className="text-gray-500">· conf {(resp.confidence*100).toFixed(0)}%</span></div>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {resp.predictions.map((p:any)=> (
                            <PredictionCard key={p.player_id} name={p.name} team={p.team} position={p.position} points={p.points} />
                        ))}
                    </div>
                </div>
            )}
        </div>
    )
}