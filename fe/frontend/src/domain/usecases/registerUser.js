export const registerUser = async (authRepo, { user_name, user_password, email }) => {
    return await authRepo.register(user_name, user_password, email);
};
