// API utility functions
const API = {
    // Get CSRF token from cookie
    getCSRFToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },

    // Generic API call function
    async call(endpoint, method = 'GET', data = null) {
        const headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCSRFToken(),
        };

        const config = {
            method: method,
            headers: headers,
            credentials: 'same-origin'
        };

        if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
            config.body = JSON.stringify(data);
        }

        const response = await fetch(endpoint, config);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    },

    // Task-specific API calls
    tasks: {
        list: () => API.call('/api/tasks/'),
        myTasks: () => API.call('/api/tasks/my_tasks/'),
        get: (uuid) => API.call(`/api/tasks/${uuid}/`),
        create: (data) => API.call('/api/tasks/', 'POST', data),
        update: (uuid, data) => API.call(`/api/tasks/${uuid}/`, 'PUT', data),
        delete: (uuid) => API.call(`/api/tasks/${uuid}/`, 'DELETE'),
        updateStatus: (uuid, status) => API.call(`/api/tasks/${uuid}/status/`, 'PATCH', { status }),
    },

    // User-specific API calls
    user: {
        me: () => API.call('/api/users/me/'),
        updateProfile: (data) => API.call('/api/users/me/', 'PATCH', data),
    }
}; 