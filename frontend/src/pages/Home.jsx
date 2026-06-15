import React from 'react'
import Navbar from '../components/Navbar/Navbar.jsx'
import Querysection from '../components/QuerySection/Querysection.jsx'
import Popular from '../components/Popular/Popular.jsx'
import Results from '../components/Results/Results.jsx'
import { useState, useEffect } from 'react'

function Home() {
    const [loading, setloading] = useState(false)
    const [movies, setmovies] = useState([])
    useEffect(() => {
        if (movies.length > 0) {
            document.getElementById("results")?.scrollIntoView({ behavior: "smooth", })
        }
    }, [movies])
    return (
        <>
            <Navbar />
            <Querysection setmovies={setmovies} setloading={setloading} />
            <Results movies={movies} loading={loading} />
        </>
    )
}

export default Home