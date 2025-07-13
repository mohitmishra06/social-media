export interface Login{
    username:any,
    password:string,
}

export interface Change{
    id:string,
    username:any,
    password:string,
}

export interface Register{
    email:string
}

export interface Forgot{
    id:string
}

export interface OTP{
    otp:any,
    id:string
}