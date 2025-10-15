import React from 'react'
import Compare from './components/Compare'


export default function App(){
    return (
    <div className="max-w-3xl mx-auto p-6">
        <header className="mb-6">
            <h1 className="text-3xl font-bold">Fantasy Insights AI</h1>
            <p className="text-sm text-gray-600">Start/Sit with data-backed projections. Type names; no IDs needed.</p>
        </header>
        <main>
            <Compare />
        </main>
        <footer className="mt-10 text-xs text-gray-500">PPR/Half-PPR supported · QB/RB/WR/TE only</footer>
    </div>
    )
}