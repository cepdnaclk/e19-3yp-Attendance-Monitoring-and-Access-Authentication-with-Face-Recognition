import React, { useState } from 'react';

const YourComponent = () => {
  const [gender, setGender] = useState('');

  const handleGenderChange = (e) => {
    setGender(e.target.value);
  };

  return (
    <div className="mb-3" style={{ color: '#318CE7' }}>
      <label htmlFor="gender">Gender</label>
      <select
        id="gender"
        className="form-select"
        value={gender}
        onChange={handleGenderChange}
      >
        <option value="">Select gender</option>
        <option value="male">Male</option>
        <option value="female">Female</option>
        <option value="other">Other</option>
      </select>
    </div>
  );
}

export default YourComponent;
