import React from 'react'
import Navbar from '../components/Navbar/Navbar.jsx'
import Querysection from '../components/QuerySection/Querysection.jsx'
import Popular from '../components/Popular/Popular.jsx'
import Results from '../components/Results/Results.jsx'
import { useState } from 'react'

function Home() {
    const [loading, setloading] = useState(false)
    const [movies, setmovies] = useState([])
    return (
        <>
            <Navbar />
            <Querysection setmovies={setmovies} setloading={setloading} />
            <Results movies={movies} loading={loading} />
        </>
    )
}

export default Home