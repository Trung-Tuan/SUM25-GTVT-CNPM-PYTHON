export const loginUser = async (authRepo, { user_name, user_password }) => {
    return await authRepo.login(user_name, user_password);
};
