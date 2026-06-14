import React from 'react'
import "./Results.css"
import Moviecard from '../Moviecard/Moviecard'

function Results({ movies }) {

    if (movies.length == 0) {
        return null;
    }

    return (
        <div className='result-section'>
            <div className='result-header'>
                <h2>✨ Top Results</h2>
                <p>{movies.length} recommendations found</p>
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
