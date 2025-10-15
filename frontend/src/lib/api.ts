import axios from 'axios'


const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
export const API = axios.create({ baseURL })


export const compare = (payload: any) => API.post('/predict/compare', payload)


export const searchPlayers = async (q: string) => {
    if(!q) return [] as any[]
    const r = await API.get('/search/players', { params: { q } })
    return r.data.results
}