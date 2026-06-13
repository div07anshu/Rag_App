import Searchbar from './Searchbar'
import "./Querysection.css"

const Querysection = () => {
    return (
        <div className='query-section'>
            <h1>Your Movie Intelligence Assistant </h1>
            <p> Discover movies through natural language queries.</p>
            <Searchbar />
        </div>
    )
}

export default Querysection