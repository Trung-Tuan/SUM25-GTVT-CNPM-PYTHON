export class AuthRepository {
    async login(user_name, user_password) {
        const res = await fetch("http://localhost:6868/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_name, user_password })
        });
        return res.json();
    }

    async register(user_name, user_password, email) {
        const res = await fetch("http://localhost:6868/api/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_name, user_password, email })
        });
        return res.json();
    }
}
