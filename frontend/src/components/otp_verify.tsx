import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import '../styles/otp_verify.css';
import CloseIcon from "@mui/icons-material/Close";
import { API_BASE_URL } from "../config/api";

const OtpVerify = () => {

    const navigate = useNavigate();

    const [otp, setOtp] = useState("");
    const [resendCount, setResendCount] = useState(0);

    const handleClose = () => {
        navigate("/home");
    };

    // Function to resend the OTP to the user's email 
    const resendOtp = async () => {
        const email = localStorage.getItem("email_id");
        if (!email) {
            alert("No registered email found. Please login again.");
            navigate("/login");
            return;
        }

        if (resendCount >= 3) {
            alert(
                "You have exceeded the maximum number of OTP resend attempts."
            );
            return;
        }
        try {
            const payload = {
                email_id: email
            };

            const response = await axios.post(
                `${API_BASE_URL}/otp`,
                payload
            );

            setResendCount(prev => prev + 1);
            if (response.data?.otp) {
                localStorage.setItem("dev_otp", response.data.otp);
                alert(`OTP Sent Successfully. Test OTP: ${response.data.otp}`);
            } else {
                alert("OTP Sent Successfully");
            }
        }
        catch (error: any) {
            const detail = error.response?.data?.detail;
            alert(detail || "Unable to send OTP");
        }
    };
    // Function to verify the OTP entered by the user 
    const verifyOtp = async () => {
        const email = localStorage.getItem("email_id");
        if (!email) {
            alert("No email ID found. Please log in again.");
            navigate("/login");
            return;
        }
        if (!otp) {
            alert("Please enter the OTP code.");
            return;
        }

        try {
            const payload = {
                email_id: email,
                otp: otp
            };
            const response = await axios.post(`${API_BASE_URL}/verify-otp`, payload);
            
            if (response.data?.success) {
                alert(response.data.message || "Verification successful.");
                localStorage.setItem("isAuthenticated", "true");
                navigate('/home');
            } else {
                alert(response.data?.message || "Invalid OTP. Verification failed.");
            }
        }
        catch (error: any) {
            const detail = error.response?.data?.detail;
            if (detail) {
                alert(detail);
            } else {
                alert("Server Error while verifying OTP");
            }
        }
    };

    return (
        <div className="otp-verify-container">
            <div className="otp-verify-box">
                <div className="closeIcon" onClick={handleClose}>
                    <CloseIcon />
                </div>

                <h2>OTP Verification</h2>
                <p className="otp-subtitle">
                    Enter the code sent to your email address. Expires in: </p>
                <div className="email-div">
                    <div className="email-text">Enter OTP</div>
                    <input
                        className="email-input"
                        type="text"
                        value={otp}
                        onChange={(e) => setOtp(e.target.value)}
                        placeholder="Enter OTP"
                    />
                </div>

                <div className="login-button-div">
                    <button className="login-button" onClick={verifyOtp}>
                        Verify OTP
                    </button>
                </div>

                <div className="signup-created">
                    <button className="account-created-button resend-otp-button" onClick={resendOtp}>
                        Resend OTP
                    </button>
                </div>
            </div>
        </div>
    );
};

export default OtpVerify;