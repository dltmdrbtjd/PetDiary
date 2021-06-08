(function() {
	const $password = document.getElementsByName('user-password')[0]

	function checkPassword() {
		const password = $password.value
		const $checkList = document.querySelectorAll('.check-list > li')

		// Set to default
		$checkList.forEach($li => {
			$li.style.color = 'red'
			$li.firstChild.textContent = '❌'
		})

		// 1. At least 8 letters
		if (password.length >= 8) {
			$checkList[0].style.color = 'green'
			$checkList[0].firstChild.textContent = '✔'
		}

		// 2. At least one uppercase letter
		if (/[A-Z]/.test(password)) {
			$checkList[1].style.color = 'green'
			$checkList[1].firstChild.textContent = '✔'
		}
		// 3. At least one lowercase letter
		if (/[a-z]/.test(password)) {
			$checkList[2].style.color = 'green'
			$checkList[2].firstChild.textContent = '✔'
		}
		// 4. At least one number
		if (/\d/.test(password)) {
			$checkList[3].style.color = 'green'
			$checkList[3].firstChild.textContent = '✔'
		}
		// 5. At leat one special character
		if (/[^A-Za-z0-9]/.test(password)) {
			$checkList[4].style.color = 'green'
			$checkList[4].firstChild.textContent = '✔'
		}

		// Check wether valid
		if([...$checkList].every($li => $li.firstChild.textContent === '✔')) {
			document.querySelector('#password-section > .check').style.visibility = 'visible'
		}
	}
	$password.addEventListener('input', checkPassword)
})()
