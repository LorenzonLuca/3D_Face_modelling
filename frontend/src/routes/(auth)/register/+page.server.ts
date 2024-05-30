import type { Actions } from './$types';
import { PUBLIC_BACKEND_URL } from "$env/static/public";
import axios, { type AxiosRequestConfig } from 'axios';
import { redirect } from '@sveltejs/kit';
import * as https from 'https'

export const actions: Actions = {
    default: async ({ cookies, request }) => {
        const data = await request.formData();
        const username = data.get('username')?.toString();
        const password = data.get('password')?.toString();
        const confPassword = data.get('password2')?.toString();

        if (username == undefined || password == undefined || confPassword == undefined) {
            return { msg: 'Please fill all the fields' }
        }

        if (username === "" || password === "" || confPassword === "") {
            return { msg: 'Please fill all the fields' }
        }

        if (password !== confPassword) {
            return { msg: 'Please insert the same password two times' }
        }

        const url = PUBLIC_BACKEND_URL + '/api/register';
        const config: AxiosRequestConfig = {
            method: 'post',
            url: url,
            headers: { "Content-Type": "multipart/form-data" },
            data: {
                username: username,
                password: password
            },
            httpsAgent: new https.Agent({
                rejectUnauthorized: false
            })
        }

        const res: AuthResponse = await axios(config)
            .then((res) => {
                cookies.set('token', res.data.token, {
                    path: '/',
                    maxAge: 60 * 60 * 24 * 30
                })
                return { 'status': true };
            })
            .catch((err) => {
                return { 'status': false, 'error': err };
            })
        if (res.status) {
            throw redirect(302, '/');
        } else {
            return errorMessage(res.error.response.status, res.error.response.data.msg)
        }
    }
}
function errorMessage(statusCode: number, msg?: string) {
    switch (statusCode) {
        case 400:
            switch (msg) {
                case "username-length-invalid":
                    return { msg: 'Username length is not valid. Username must be min 5 characters and at max 20' }
                case "password-invalid":
                    return { msg: 'Password is not valid. Password must be long at min 6 characters and contain one number and one special char' }
                case "user-exist":
                    return { msg: 'This user already exists. Change username' }
            }
    }
}