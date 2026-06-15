import React from 'react'
import "./Results.css"
import Moviecard from '../Moviecard/Moviecard'

function Results({ movies, loading }) {
    console.log("Loading:", loading);
    console.log("Movies:", movies);

    if (loading) {
        return (
            <div className='loading-state' >
                <div className='spinner'></div>
                <h2>Understanding your movie request...</h2>
            </div >
        )
    }

    if (movies.length == 0) {
        return null;
    }

    return (
        <div className='results-section' id='results'>
            <div className='results-header'>
                <h2>✨ Top Results</h2>
            </div>
            <div className='result-container'>
                {movies.map((movie, index) => (
                    <Moviecard
                        key={index}
                        movie={movie}
                    />

                ))}
            </div>
        </div>
    )
}

export default Results
