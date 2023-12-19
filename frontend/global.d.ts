declare module '*.jpg';
declare module '*.png';
declare module "*.css";
// declare module "*.scss";
// declare module "*.module.scss";
declare let XDomainRequest;
declare module "*.scss" {
    const styles: { [className: string]: string };
    export default styles;
}
