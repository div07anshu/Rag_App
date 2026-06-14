import Searchbar from './Searchbar'
import { useState } from 'react'
import "./Querysection.css"

const Querysection = ({ setmovies }) => {

    return (
        <div className='query-section'>
            <h1>Your Movie Intelligence Assistant </h1>
            <p> Discover movies through natural language queries.</p>
            <Searchbar setmovies={setmovies} />
        </div>
    )
}

export default Querysection