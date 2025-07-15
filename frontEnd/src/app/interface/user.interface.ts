export interface User{
    id:any,
    userId:any,
    username:string,
    email:string,
    img:string,
    banner:string,
    name:string,
    surname:string,
    desc:string,
    city:string,
    school:string,
    work:string,
    website:string,
    followers:number,
    following:number,
    posts:number,
    likes:number,
    comments:number,
    block:boolean,
    created_at:Date,
}

export interface UpdatePersonalDetails{
    name:string,
    surname:string,
    email:string,
    desc:string,
    city:string,
    school:string,
    work:string,
    website:string,
}

export interface ChangePasswordDetails{
    username:any,
    password:any
}

export interface updateProfilePicture{
    img:any
}

export interface updateBannerImage{
    banner:any
}