// <summary>
// <copyright file="TestsDao.cs" company="Axity">
// This source code is Copyright Axity and MAY NOT be copied, reproduced,
// published, distributed or transmitted to or stored in any manner without prior
// written consent from Axity (www.axity.com).
// </copyright>
// </summary>

namespace Toks.Loyalty.test.Persistence.DAO.Tests.Impl
{
    /// <summary>
    /// Class TestsDao.
    /// </summary>
    public class TestsDao : ITestsDao
    {
        private readonly DatabaseContext context;

        /// <summary>
        /// Initializes a new instance of the <see cref="TestsDao"/> class.
        /// </summary>
        /// <param name="context">DataBase Context.</param>
        public TestsDao(DatabaseContext context)
        {
            ArgumentNullException.ThrowIfNull(context);
            this.context = context;
        }

        /// <inheritdoc/>
        public async Task<int> SaveChangesAsync() => await this.context.SaveChangesAsync();
    }
}
