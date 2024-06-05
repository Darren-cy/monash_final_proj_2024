import { useState, useEffect } from 'react'
import api from '../api';
const Profile = () => {
    const [user, setUser] = useState<{name: string, email: string} | null>(null);

    useEffect(() => {
        // Fetch user data based on the user name from the backend
        const fetchUser = async () => {
            try {
                const response = await api.get('/api/v1.0/profile');
                const data = await response.data;
                setUser(data);
            } catch (error) {
                console.error('Error fetching user data:', error);
                alert('Error fetching user data');
            }
        };

        fetchUser();
    }, []);

    if (!user) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>Profile</h1>
            <p>Name: {user.name}</p>
            <p>Email: {user.email}</p>
        </div>
    );
};

export default Profile;