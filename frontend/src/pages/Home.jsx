import React from 'react'
import Navbar from '../components/Navbar/Navbar.jsx'
import Querysection from '../components/QuerySection/Querysection.jsx'
import Popular from '../components/Popular/Popular.jsx'
import Results from '../components/Results/Results.jsx'
import { useState } from 'react'

function Home() {
    const [movies, setmovies] = useState([])
    return (
        <>
            <Navbar />
            <Querysection setmovies={setmovies} />
            <Results movies={movies} />
        </>
    )
}

export default Home